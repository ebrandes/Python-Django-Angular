import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, switchMap, tap } from 'rxjs';
import { User } from '../../@types/user';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  http = inject(HttpClient);
  router = inject(Router);

  login(email: string, password: string): Observable<User> {
    return this.http.post<User>(`${environment.apiBaseUrl}/auth/login/`, {
      email,
      password,
    });
  }

  logout(): Observable<void> {
    return this.http
      .post<void>(`${environment.apiBaseUrl}/auth/logout/`, {
        withCredentials: true,
      })
      .pipe(
        tap(() => {
          console.log('Logged out successfully');
          window.location.href = '/login';
        })
      );
  }

  private getRefreshToken(): string | null {
    return (
      document.cookie
        .split('; ')
        .find((row) => row.startsWith('refresh_token='))
        ?.split('=')[1] || null
    );
  }
}
