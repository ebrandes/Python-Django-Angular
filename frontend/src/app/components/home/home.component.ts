import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Product } from '../../@types/product';
import { ProductsService } from '../../services/products/products.service';
import { AuthenticationService } from '../../services/authentication/authentication.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  products: Product[] = [];

  authService = inject(AuthenticationService);
  productService = inject(ProductsService);

  ngOnInit() {
    this.productService.getProducts().subscribe((products) => {
      this.products = products;
    });
  }

  logout() {
    this.authService.logout().subscribe(() => {});
  }
}
