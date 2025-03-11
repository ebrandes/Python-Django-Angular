import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class StorageService {
  private isBrowser(): boolean {
    return typeof window !== 'undefined';
  }

  setItem(key: string, value: any): void {
    if (this.isBrowser()) {
      sessionStorage.setItem(key, JSON.stringify(value));
    }
  }

  getItem<T>(key: string): T | null {
    if (!this.isBrowser()) {
      return null;
    }

    const data = sessionStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  }

  removeItem(key: string): void {
    if (this.isBrowser()) {
      sessionStorage.removeItem(key);
    }
  }
}
