import { Component, inject, OnInit, Type } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { PopoverModule } from 'primeng/popover';
import { DrawerModule } from 'primeng/drawer';
import { CartComponent } from '../cart/cart.component';
import { AuthenticationService } from '../../services/authentication/authentication.service';
import { ToastService } from '../../services/toast/toast.service';
import { CommonModule } from '@angular/common';
import { CartService } from '../../services/cart/cart.service';
@Component({
  selector: 'app-header',
  imports: [CommonModule, DrawerModule, ButtonModule, PopoverModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent implements OnInit {
  // visible: boolean = false;
  authenticationService = inject(AuthenticationService);
  cartService = inject(CartService);
  toastService = inject(ToastService);
  user$ = this.authenticationService.user$;
  cartIsVisible$ = this.cartService.cartIsVisible$;

  cartComponent?: Type<CartComponent>;

  constructor() {
    import('../cart/cart.component').then((module) => {
      this.cartComponent = module.CartComponent;
    });
  }

  ngOnInit(): void {
    this.authenticationService.getCurrentUser().subscribe();
  }

  toggleCart() {
    this.cartService.toggleCart();
  }

  logout() {
    this.authenticationService.logout().subscribe(() => {
      this.toastService.showSuccess('Logged out', 'You are now logged out');
    });
  }
}
