import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { User } from '../../@types/user';
import { StorageService } from '../session-storage/session-storage.service';
import { UserResponse } from './@types/user.response';

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
      .get<UserResponse>(`${environment.apiBaseUrl}/api/users/me/`, {
        withCredentials: true,
      })
      .pipe(
        tap((userResponse) => {
          const user = this.userResponseToUser(userResponse);
          this.setUserInSession(user);
          this.userSubject.next(user);
        }),
        map((userResponse) => this.userResponseToUser(userResponse)),
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
        tap((_) => {
          this.getCurrentUser().subscribe();
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

  refreshToken(): Observable<User> {
    return this.http.post<User>(
      `${environment.apiBaseUrl}/api/auth/refresh/`,
      {},
      {
        withCredentials: true,
      }
    );
  }

  private userResponseToUser(response: UserResponse): User {
    return {
      id: response.user_id,
      email: response.email,
      firstName: response.first_name,
      lastName: response.last_name,
      role: response.role,
    };
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
