import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import {
  FormBuilder,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import { AuthenticationService } from '../../services/authentication/authentication.service';
import { User } from '../../@types/user';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [FormsModule, ReactiveFormsModule, CommonModule],
  providers: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  authenticationService = inject(AuthenticationService);
  fb = inject(FormBuilder);
  router = inject(Router);

  loginForm = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required],
  });

  onSubmit(): void {
    const email = this.loginForm.get('email')?.value;
    const password = this.loginForm.get('password')?.value;

    if (email && password) {
      this.authenticationService.login(email, password).subscribe({
        next: (user: User) => {
          console.log(user);
          this.router.navigate(['/home']);
        },
        error: (err) => {},
      });
    }
  }
}
