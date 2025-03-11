import { inject, Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthenticationService } from '../services/authentication/authentication.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  authenticationService = inject(AuthenticationService);
  router = inject(Router);

  canActivate(): Observable<boolean> {
    return this.authenticationService.getCurrentUser().pipe(
      map((user) => {
        if (user) {
          return true;
        }
        return false;
      })
    );
  }
}
