import { inject, Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthenticationService } from '../services/authentication/authentication.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  authenticationService = inject(AuthenticationService);
  router = inject(Router);

  canActivate(): boolean {
    return true;
  }
}
