import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

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
  matinanceRequests: number = 0;
  numberOfRooms: number = 0;
  occupiedRooms: number = 0;

  dashboadView: boolean = true;
  manageRoomView: boolean = false;
  studentsView: boolean = false;

  recentBookings: BookingData[] = [];
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchAdminData();
  }

  fetchAdminData(): void {
    this.http.get<AdminDataResponse>(`${this.apiUrl}/fetch_admin_data`).subscribe({
      next: (response) => {
        console.log('Admin data received:', response);
        
        // Map booking data to display format
        this.recentBookings = response.bookings.map(booking => ({
          id: booking.id,
          student_id: booking.student_id,
          lease_length: booking.lease_length,
          dorm_name: booking.dorm_name, 
          room_number: booking.room_number,
          confirmed: booking.confirmed,
        }));
        
        // Count pending requests
        this.pendingRequests = this.recentBookings.filter(b => b.confirmed === false || b.confirmed === null).length;
        
        // Set other dashboard stats (would come from backend in a full implementation)
        this.totalStudents = this.recentBookings.length;
      },
      error: (error) => {
        console.error('Error fetching admin data:', error);
      }
    });
  }

  confirmBooking(bookingId: number): void {
    this.http.post(`${this.apiUrl}/confirm_booking`, { booking_id: bookingId, confirmed: true })
      .subscribe({
        next: () => {
          // Update local booking status
          const booking = this.recentBookings.find(b => b.id === bookingId);
          if (booking) {
            booking.confirmed = true;
          }
          this.pendingRequests = this.recentBookings.filter(b => b.confirmed === false).length;
        },
        error: (error) => {
          console.error('Error confirming booking:', error);
        }
      });
  }

  denyBooking(bookingId: number): void {
    this.http.post(`${this.apiUrl}/confirm_booking`, { booking_id: bookingId, confirmed: false })
      .subscribe({
        next: () => {
          // Update local booking status
          const booking = this.recentBookings.find(b => b.id === bookingId);
          if (booking) {
            booking.confirmed = false;
          }
          this.pendingRequests = this.recentBookings.filter(b => b.confirmed === false).length;
        },
        error: (error) => {
          console.error('Error denying booking:', error);
        }
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

interface BookingData {
  id: number;
  student_id: string;
  lease_length: number;
  dorm_name: string;
  room_number: string;
  confirmed: boolean | null;
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
}

interface RecentBooking{
  studentInfo: Student
  roomNumber: number;
  checkInDate: Date;
  checkOutDate: Date;
  approvalStatus: boolean;
  building: string;
}

interface Room {
  roomNumber: number;
  building: string;
  occupancy: number;
  status: string;
  maintenance: boolean;
  studentId: string;
}

interface Student {
  studentId: string;
  studentName: string;
}