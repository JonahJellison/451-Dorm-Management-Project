import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUser: any = null; // Store user data

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {
    // Initialize user data if in browser environment
    if (isPlatformBrowser(this.platformId)) {
      this.currentUser = JSON.parse(localStorage.getItem('user') || 'null');
    }
  }

  setUser(user: any) {
    this.currentUser = user;
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem('user', JSON.stringify(user));
    }
  }

  getUser() {
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return this.getUser() !== null;
  }

  logout() {
    this.currentUser = null;
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('user');
    }
  }
}
