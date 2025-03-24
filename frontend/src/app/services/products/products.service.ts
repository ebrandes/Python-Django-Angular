import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import { map, Observable } from 'rxjs';
import { Product } from '../../@types/product';
import { ProductResponse } from './@types/products.types';

@Injectable({
  providedIn: 'root',
})
export class ProductsService {
  http = inject(HttpClient);

  getProducts(): Observable<Product[]> {
    return this.http
      .get<ProductResponse[]>(`${environment.apiBaseUrl}/api/products/`, {
        withCredentials: true,
      })
      .pipe(
        map((products) =>
          products.map((product) => this.productResponseToProduct(product))
        )
      );
  }

  private productResponseToProduct(response: ProductResponse): Product {
    return {
      id: response.id,
      name: response.name,
      description: response.description,
      price: response.price,
      isAvailable: response.isAvailable,
    };
  }
}
