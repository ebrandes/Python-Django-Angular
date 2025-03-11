import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { User } from '../../@types/user';
import { StorageService } from '../session-storage/session-storage.service';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  private userSubject = new BehaviorSubject<User | null>(
    this.getUserFromSession()
  );

  user$: Observable<User | null> = this.userSubject.asObservable();
  sessionStorage = inject(StorageService);
  router = inject(Router);

  constructor(private http: HttpClient) {}

  getCurrentUser(): Observable<User | null> {
    if (this.userSubject.value) {
      return of(this.userSubject.value);
    }

    return this.http
      .get<User>(`${environment.apiBaseUrl}/api/users/me/`, {
        withCredentials: true,
      })
      .pipe(
        tap((user) => {
          this.setUserInSession(user);
          this.userSubject.next(user);
        }),
        catchError(() => {
          this.clearSession();
          this.userSubject.next(null);
          return of(null);
        })
      );
  }

  login(email: string, password: string): Observable<User> {
    return this.http
      .post<User>(
        `${environment.apiBaseUrl}/api/auth/login/`,
        { email, password },
        { withCredentials: true }
      )
      .pipe(
        tap((user) => {
          this.setUserInSession(user);
          this.userSubject.next(user);
        })
      );
  }

  logout(): Observable<Object> {
    return this.http
      .post(
        `${environment.apiBaseUrl}/api/auth/logout/`,
        {},
        { withCredentials: true }
      )
      .pipe(
        tap(() => {
          this.clearSession();
          this.userSubject.next(null);
          this.router.navigate(['/login']);
        })
      );
  }

  private setUserInSession(user: User) {
    this.sessionStorage?.setItem('user', JSON.stringify(user));
  }

  private getUserFromSession(): User | null {
    const userData = this.sessionStorage?.getItem<User>('user');
    return userData ? userData : null;
  }

  private clearSession() {
    this.sessionStorage?.removeItem('user');
  }
}
