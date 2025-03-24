import { Component, inject, OnInit } from '@angular/core';
import { Cart } from '../../@types/cart';
import { Product } from '../../@types/product';
import { CartService } from '../../services/cart/cart.service';
import { CommonModule } from '@angular/common';
import { ToastService } from '../../services/toast/toast.service';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-cart',
  imports: [CommonModule, ButtonModule],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.scss',
})
export class CartComponent implements OnInit {
  cartService = inject(CartService);
  toastService = inject(ToastService);
  cart$ = this.cartService.cart$;

  ngOnInit(): void {
    this.cartService.getCart().subscribe();
  }

  checkout() {
    this.cartService.checkout().subscribe({
      next: () => {
        this.toastService.showSuccess(
          'Checkout successful',
          'You have successfully checked out'
        );
      },
      error: () => {
        this.toastService.showError(
          'Error',
          'An error occurred while checking out'
        );
      },
    });
  }

  removeFromCart(item: Product) {
    this.cartService.removeFromCart(item.id).subscribe({
      next: () => {
        this.toastService.showSuccess(
          'Removed from cart',
          'Product removed from cart'
        );
      },
      error: () => {
        this.toastService.showError(
          'Error',
          'An error occurred while removing the product from cart'
        );
      },
    });
  }
}
