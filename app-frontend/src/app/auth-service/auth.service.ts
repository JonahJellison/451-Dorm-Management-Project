import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUser: any = null; // Store user data

  constructor() {}

  setUser(user: any) {
    this.currentUser = user;
    localStorage.setItem('user', JSON.stringify(user)); // Persist user data if needed
    
  }

  getUser() {
    if (!this.currentUser) {
      this.currentUser = JSON.parse(localStorage.getItem('user') || 'null');
    }
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return this.getUser() !== null;
  }

  logout() {
    this.currentUser = null;
    localStorage.removeItem('user');
  }
}
