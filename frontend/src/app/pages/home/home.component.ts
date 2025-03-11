import { Component, inject, OnInit, ViewEncapsulation } from '@angular/core';
import { AuthenticationService } from '../../services/authentication/authentication.service';
import { ButtonModule } from 'primeng/button';
import { ToastService } from '../../services/toast/toast.service';
import { DrawerModule } from 'primeng/drawer';
import { CartComponent } from '../../components/cart/cart.component';
import { CommonModule } from '@angular/common';
import { Product } from '../../@types/product';
import { ProductsService } from '../../services/products/products.service';
import { CardModule } from 'primeng/card';
import { CartService } from '../../services/cart/cart.service';

@Component({
  selector: 'app-home',
  imports: [
    CommonModule,
    ButtonModule,
    DrawerModule,
    CardModule,
    CartComponent,
  ],
  templateUrl: './home.component.html',
  encapsulation: ViewEncapsulation.None,
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit {
  authenticationService = inject(AuthenticationService);
  productService = inject(ProductsService);
  cartService = inject(CartService);
  toastService = inject(ToastService);

  visible: boolean = false;

  products: Product[] = [];

  ngOnInit(): void {
    this.productService.getProducts().subscribe({
      next: (products) => (this.products = products),
      error: () => {
        this.toastService.showError(
          'Error',
          'An error occurred while fetching products'
        );
      },
    });
  }

  logout() {
    this.authenticationService.logout().subscribe(() => {
      this.toastService.showSuccess('Logged out', 'You are now logged out');
    });
  }

  addToCart(product: Product) {
    this.cartService.addToCart(product.id, 1).subscribe({
      next: () => {
        this.toastService.showSuccess('Added to cart', 'Product added to cart');
      },
      error: () => {
        this.toastService.showError(
          'Error',
          'An error occurred while adding the product to cart'
        );
      },
    });
  }
}
