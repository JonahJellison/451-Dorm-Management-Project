import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { AuthService } from '../auth-service/auth.service';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-dorm-bookings',
  templateUrl: './dorm-bookings.component.html',
  styleUrls: ['./dorm-bookings.component.css'],
  imports: [CommonModule, FormsModule, HttpClientModule],
  standalone: true
})
export class DormBookingsComponent implements OnInit, OnDestroy {
  studentId: string | null = null;

  selectedBuilding   = '';
  selectedRoomType   = '';
  selectedPriceRange = '';

  duncan_img    = "/duncan_dunn.jpg";
  global_img    = "/global_scholars.jpg";
  honors_img    = "/honors.jpg";
  northside_img = "/northside.jpg";

  selected_dorms: Room[] = [];
  selectedRoomForBooking: Room | null = null;
  showBookingPopup = false;
  requestRoommate  = false;
  roommateStudentId = '';
  leaseDuration    = 6; // Default to 6 months

  private pollSub?: Subscription;

  constructor(
    private http: HttpClient,
    private authservice: AuthService
  ) {}

  ngOnInit(): void {
    this.studentId = this.authservice.getUser();
    console.log('On dorm booking page with Student ID:', this.studentId);

    // load immediately
    this.applyFilters();

    // then poll every 5 seconds
    this.pollSub = interval(5000).subscribe(() => {
      this.applyFilters();
    });
  }

  ngOnDestroy(): void {
    // stop polling when component is destroyed
    this.pollSub?.unsubscribe();
  }

  getDormImage(dormName: string): string {
    switch (dormName.toLowerCase()) {
      case 'duncan dunn':     return this.duncan_img;
      case 'global scholars': return this.global_img;
      case 'honors hall':     return this.honors_img;
      case 'northside':       return this.northside_img;
      default: return '';
    }
  }

  applyFilters(): void {
    const filters = {
      building:   this.selectedBuilding   || 'All',
      roomType:   this.selectedRoomType   || 'All',
      priceRange: this.selectedPriceRange || 'All'
    };

    console.log('Filtering with', filters);

    interface RoomResponse { rooms: Room[]; }

    this.http.get<RoomResponse>(
      'http://127.0.0.1:8000/api/fetch_dormroom_data',
      { params: filters }
    ).subscribe(
      res => {
        this.selected_dorms = res.rooms;
        console.log('Fetched dorms:', this.selected_dorms);
      },
      err => console.error('Error fetching dorms', err)
    );
  }

  openBookingPopup(room: Room): void {
    this.selectedRoomForBooking = room;
    this.showBookingPopup = true;
    this.requestRoommate = false;
    this.roommateStudentId = '';
    this.leaseDuration = 6;
  }

  closeBookingPopup(): void {
    this.showBookingPopup = false;
    this.selectedRoomForBooking = null;
  }

  submitBooking(): void {
    if (!this.selectedRoomForBooking) return;

    const bookingData = {
      student_id: this.studentId,
      room_id: this.selectedRoomForBooking.room_id,
      request_roommate: this.requestRoommate,
      roommate_student_id: this.requestRoommate ? this.roommateStudentId : null,
      lease_duration: this.leaseDuration
    };

    console.log('Submitting booking:', bookingData);

    this.http.post('http://127.0.0.1:8000/api/book_room', bookingData)
      .subscribe(
        () => {
          alert('Room booked successfully!');
          this.closeBookingPopup();
        },
        err => {
          console.error('Booking error', err);
          alert('Error booking room. Please try again.');
        }
      );
  }
}

export interface Room {
  room_id: number;
  dorm_name: string;
  room_number: string;
  capacity: number;
  has_AC: boolean;
  has_private_bath: boolean;
  cost_per_month: number;
}
