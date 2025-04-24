import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../auth-service/auth.service';
@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrl: './admin-dashboard.component.css'
})
export class AdminDashboardComponent implements OnInit {

  totalStudents: number = 0;
  occupancyRate: number = 0;
  pendingRequests: number = 0;
  maintenanceRequests: number = 0;
  numberOfRooms: number = 0;
  occupiedRooms: number = 0;
  maintenanceList: MaintenanceRequestData[] = [];

  dashboadView: boolean = true;
  manageRoomView: boolean = false;
  studentsView: boolean = false;

  recentBookings: BookingData[] = [];
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) {}

  ngOnInit(): void {
    if (this.authService.getUser() == null){
      this.router.navigate(['/home']);
      return;
    }
    this.http.post<boolean> (`${this.apiUrl}/verify_admin`, {id: this.authService.getUser()}).subscribe({
      next: (isAdmin) => {
        if (!isAdmin) {
          console.error('User is not an admin');
          this.router.navigate(['/home']);
          return;
        }
        console.log('Admin Dashboard Component Initialized with user:', this.authService.getUser());

      },
      error: (error) => {
        console.error('Error checking admin status:', error);
      }
    });
    this.fetchAdminData();
  }

  // get all the admin data from the backend
  fetchAdminData(): void {
    this.http.get<AdminDataResponse>(`${this.apiUrl}/fetch_admin_data`).subscribe({
      next: (response) => {
        console.log('Admin data received:', response);
        
        // Map booking data to include fields used in the HTML template
        this.recentBookings = response.bookings.map(booking => ({
          id: booking.id,
          student_id: booking.student_id,
          lease_length: booking.lease_length,
          dorm_name: booking.dorm_name,
          room_number: booking.room_number,
          confirmed: booking.confirmed,
          student_name: 'John Doe', // Replace with actual data if available
          building: booking.dorm_name,
          date: booking.booking_date,
          status: booking.confirmed === null
            ? 'Pending'
            : booking.confirmed === true
              ? 'Confirmed'
              : 'Denied'
        }));
        
        this.pendingRequests = this.recentBookings.filter(b => b.status === 'Pending').length;
        this.totalStudents = this.recentBookings.length;
        // update maintenance and room stats
        this.maintenanceList = response.maintenance_requests;
        this.maintenanceRequests = this.maintenanceList.length;
        this.occupiedRooms = response.occupied_rooms.length;
        this.numberOfRooms = response.occupied_rooms.length;
      },
      error: (error) => {
        console.error('Error fetching admin data:', error);
      }
    });
  }

  confirmBooking(bookingId: number): void {
    const booking = this.recentBookings.find(b => b.id === bookingId);
    if (!booking) { return; }
    this.http.post(`${this.apiUrl}/confirm_booking`, { booking_id: bookingId, student_id: booking.student_id })
      .subscribe({
        next: () => {
          if (booking) {
            booking.confirmed = true;
            booking.status = 'Confirmed';
          }
          this.pendingRequests = this.recentBookings.filter(b => b.status === 'Pending').length;
        },
        error: (error) => {
          console.error('Error confirming booking:', error);
        }
      });
  }

  denyBooking(bookingId: number): void {
    const booking = this.recentBookings.find(b => b.id === bookingId);
    if (!booking) { return; }
    this.http.post(`${this.apiUrl}/deny_booking`, { booking_id: bookingId, student_id: booking.student_id })
      .subscribe({
        next: () => {
          if (booking) {
            booking.confirmed = false;
            booking.status = 'Denied';
          }
          this.pendingRequests = this.recentBookings.filter(b => b.status === 'Pending').length;
        },
        error: (error) => {
          console.error('Error denying booking:', error);
        }
      });
  }

  deleteMaintenanceRequest(requestId: number): void {
    const studentId = this.authService.getUser();
    this.http.delete(`${this.apiUrl}/delete_maintenance_request`, { body: { request_id: requestId, student_id: studentId } })
      .subscribe({
        next: () => {
          this.maintenanceRequests = Math.max(this.maintenanceRequests - 1, 0);
        },
        error: (error) => console.error('Error deleting maintenance request:', error)
      });
  }

  setDashboardView() {
    this.dashboadView = true;
    this.manageRoomView = false;
    this.studentsView = false;
  }

  setManageRoomView() {
    this.dashboadView = false;
    this.manageRoomView = true;
    this.studentsView = false;
  }

  setStudentsView() {
    this.dashboadView = false;
    this.manageRoomView = false;
    this.studentsView = true;
  }
}

// interfaces to match data models from the backend
interface BookingData {
  id: number;
  student_id: string;
  lease_length: number;
  dorm_name: string;
  room_number: string;
  confirmed: boolean | null;

  student_name: string;
  building: string;
  date: string | null;
  status: 'Pending' | 'Confirmed' | 'Denied';
}

interface AdminDataResponse {
  bookings: {
    id: number;
    student_id: string;
    booking_date: string | null;
    lease_length: number;
    dorm_name: string;
    room_number: string;
    confirmed: boolean | null;
  }[];
  maintenance_requests: {
    id: number;
    student_id: string;
    issue: string;
    location: string;
    priority: string;
    date_created: string;
  }[];
  occupied_rooms: {
    room_id: number;
    dorm_name: string;
    room_number: string;
    capacity: number;
    current_occupants: number;
  }[];
}

interface MaintenanceRequestData {
  id: number;
  student_id: string;
  issue: string;
  location: string;
  priority: string;
  date_created: string;
}
