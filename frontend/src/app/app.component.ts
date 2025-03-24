import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { ToastService } from './services/toast/toast.service';
import { HeaderComponent } from './components/header/header.component';
@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, ToastModule, HeaderComponent],
  providers: [ToastService, MessageService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  private router = inject(Router);
  currentRoute = signal(this.router.url);

  routesToExcludeHeader = ['/login', '/register'];

  constructor() {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.currentRoute.set(event.urlAfterRedirects);
      }
    });
  }

  showHeader = computed(() => {
    return !this.routesToExcludeHeader.includes(this.currentRoute());
  });
}
