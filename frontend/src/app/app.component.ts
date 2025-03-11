import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { ToastService } from './services/toast/toast.service';
import { MessageService } from 'primeng/api';
@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, ToastModule],
  providers: [ToastService, MessageService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {}
