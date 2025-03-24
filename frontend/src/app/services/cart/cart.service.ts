import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BehaviorSubject, map, Observable, tap } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { Address } from '../../@types/address';
import { Card } from '../../@types/card';
import { Cart } from '../../@types/cart';
import {
  CartAddressResponse,
  CartCardResponse,
  CartProductResponse,
  CartResponse,
} from './@types/cart.response';
import { Product } from '../../@types/product';

@Injectable({
  providedIn: 'root',
})
export class CartService {
  private cartSubject = new BehaviorSubject<Cart | null>(null);
  cart$ = this.cartSubject.asObservable();

  private cartIsVisibleSubject = new BehaviorSubject<boolean>(false);
  cartIsVisible$ = this.cartIsVisibleSubject.asObservable();

  http = inject(HttpClient);

  getCart(): Observable<Cart> {
    return this.http
      .get<CartResponse>(`${environment.apiBaseUrl}/api/cart/`, {
        withCredentials: true,
      })
      .pipe(
        map((cartResponse) => this.cartResponseToCart(cartResponse)),
        tap((cart) => this.cartSubject.next(cart))
      );
  }

  checkout(): Observable<void> {
    return this.http
      .post<void>(`${environment.apiBaseUrl}/api/cart/checkout`, null, {
        withCredentials: true,
      })
      .pipe(tap(() => this.getCart().subscribe()));
  }

  addToCart(productId: number, quantity: number): Observable<Cart> {
    return this.http
      .post<CartResponse>(
        `${environment.apiBaseUrl}/api/cart/add/`,
        { product_id: productId, quantity },
        {
          withCredentials: true,
        }
      )
      .pipe(
        map((cartResponse) => this.cartResponseToCart(cartResponse)),
        tap((cart) => {
          this.cartSubject.next(cart);
          this.cartIsVisibleSubject.next(true);
        })
      );
  }

  removeFromCart(productId: number): Observable<void> {
    return this.http
      .delete<void>(`${environment.apiBaseUrl}/api/cart/remove/${productId}/`, {
        withCredentials: true,
      })
      .pipe(tap(() => this.getCart().subscribe()));
  }

  openCart(): void {
    this.cartIsVisibleSubject.next(true);
  }

  closeCart(): void {
    this.cartIsVisibleSubject.next(false);
  }

  toggleCart(): void {
    this.cartIsVisibleSubject.next(!this.cartIsVisibleSubject.value);
  }

  private cartResponseToCart(response: CartResponse): Cart {
    return {
      user: response.user,
      totalPrice: response.total_price,
      items: this.cartProductResponseToProduct(response.items),
      address: this.cartAddressResponseToAddress(response.address),
      paymentCard: this.cartCardResponseToCard(response.payment_card),
    };
  }

  private cartProductResponseToProduct(
    response?: CartProductResponse[]
  ): Product[] | undefined {
    if (!response) return undefined;
    return response.map((item) => ({
      id: item.id,
      name: item.product_name,
      description: item.product_description,
      price: item.product_price,
      isAvailable: item.product_is_available,
      quantity: item.quantity,
      totalPrice: item.total_price,
    }));
  }

  private cartAddressResponseToAddress(
    response?: CartAddressResponse
  ): Address | undefined {
    if (!response) return undefined;
    return {
      id: response.id,
      user: response.user,
      street: response.street,
      city: response.city,
      state: response.state,
      zipCode: response.zipCode,
      country: response.country,
      active: response.active,
      selected: response.selected,
    };
  }

  private cartCardResponseToCard(
    response?: CartCardResponse
  ): Card | undefined {
    if (!response) return undefined;
    return {
      id: response.id,
      user: response.user,
      lastFourDigits: response.last_four_digits,
      holder: response.holder,
      expiryYear: response.expiry_year,
      expiryMonth: response.expiry_month,
      brand: response.brand,
    };
  }
}
