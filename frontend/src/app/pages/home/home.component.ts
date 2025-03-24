import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ViewEncapsulation } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { Product } from '../../@types/product';
import { CartService } from '../../services/cart/cart.service';
import { ProductsService } from '../../services/products/products.service';
import { ToastService } from '../../services/toast/toast.service';

@Component({
  selector: 'app-home',
  imports: [CommonModule, ButtonModule, CardModule],
  templateUrl: './home.component.html',
  encapsulation: ViewEncapsulation.None,
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit {
  productService = inject(ProductsService);
  cartService = inject(CartService);
  toastService = inject(ToastService);

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

  addToCart(product: Product) {
    this.cartService.addToCart(product.id, 1).subscribe({
      next: () => {
        //open cart
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
