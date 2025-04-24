import { Component, OnInit }           from '@angular/core';
import { CommonModule }                from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule }                 from '@angular/forms';
import { Router }                      from '@angular/router';
import { AuthService }                 from '../auth-service/auth.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  // stats
  totalStudents   = 0;
  pendingRequests = 0;
  pendingMaint    = 0;
  occupiedCount   = 0;

  // data
  recentBookings    : BookingData[]            = [];
  maintenanceList   : MaintenanceRequestData[] = [];
  occupiedRoomsList : OccupiedRoomData[]       = [];

  // modal state
  showModal       = false;
  selectedBooking?: BookingData;
  selectedStatus: 'Pending'|'Confirmed'|'Denied' = 'Pending';

  // view toggles
  dashboadView   = true;
  manageRoomView = false;
  studentsView   = false;

  private apiUrl = 'http://localhost:8000/api';

  constructor(
    private http: HttpClient,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // your verify-admin check…
    this.fetchAdminData();
  }

  fetchAdminData(): void {
    this.http.get<AdminDataResponse>(`${this.apiUrl}/fetch_admin_data`)
      .subscribe({
        next: res => {
          // Recent Bookings
          this.recentBookings = res.bookings.map(b => ({
            id:           b.id,
            student_id:   b.student_id,
            lease_length: b.lease_length,
            dorm_name:    b.dorm_name,
            room_number:  b.room_number,
            confirmed:    b.confirmed,
            student_name: 'John Doe',       // placeholder
            building:     b.dorm_name,
            date:         b.booking_date,
            status:       b.confirmed===null
                            ? 'Pending'
                            : b.confirmed ? 'Confirmed' : 'Denied'
          }));
          this.totalStudents   = this.recentBookings.length;
          this.pendingRequests = this.recentBookings
                                   .filter(b=>b.status==='Pending')
                                   .length;

          // Maintenance Requests
          this.maintenanceList = res.maintenance_requests;
          this.pendingMaint    = this.maintenanceList
                                   .filter(m=>m.status===null)
                                   .length;

          // Occupied Rooms (confirmed bookings)
          this.occupiedRoomsList = res.occupied_rooms;
          this.occupiedCount     = this.occupiedRoomsList.length;
        },
        error: err => console.error(err)
      });
  }

  // Booking modal
  viewBooking(id: number) {
    const bk = this.recentBookings.find(b=>b.id===id);
    if (!bk) return;
    this.selectedBooking = bk;
    this.selectedStatus  = bk.status;
    this.showModal       = true;
  }

  saveBookingStatus() {
    if (!this.selectedBooking) return;
    const payload = {
      booking_id: this.selectedBooking.id,
      status:     this.selectedStatus
    };
    this.http.post(`${this.apiUrl}/update_booking`, payload)
      .subscribe(() => {
        // update in-place
        this.selectedBooking!.confirmed =
          this.selectedStatus==='Confirmed'? true
          : this.selectedStatus==='Denied'? false
          : null;
        this.selectedBooking!.status = this.selectedStatus;
        this.pendingRequests = this.recentBookings
                                 .filter(b=>b.status==='Pending')
                                 .length;
      });
    this.showModal = false;
  }

  // Maintenance Approve/Deny
  updateMaintenance(req: MaintenanceRequestData, newState: 'Approved'|'Denied') {
    this.http.post(`${this.apiUrl}/update_maintenance`, {
      request_id: req.id,
      status:     newState
    }).subscribe(() => {
      req.status = (newState==='Approved');
      this.pendingMaint = this.maintenanceList
                              .filter(m=>m.status===null)
                              .length;
    }, err => console.error(err));
  }

  // View toggles
  setDashboardView()   { this.dashboadView=true;   this.manageRoomView=this.studentsView=false; }
  setManageRoomView()  { this.manageRoomView=true;  this.dashboadView=this.studentsView=false; }
  setStudentsView()    { this.studentsView=true;    this.dashboadView=this.manageRoomView=false; }
}


// ─── interfaces ─────────────────────────────────────────────────────────

interface BookingData {
  id: number;
  student_id: string;
  lease_length: number;
  dorm_name: string;
  room_number: string;
  confirmed: boolean|null;
  student_name: string;
  building: string;
  date: string|null;
  status: 'Pending'|'Confirmed'|'Denied';
}

interface MaintenanceRequestData {
  id: number;
  student_id: string;
  issue: string;
  location: string;
  priority: string;
  date_created: string;
  status: boolean|null;  // null=Pending, true=Approved, false=Denied
}

interface OccupiedRoomData {
  id: number;           // booking_id
  student_id: string;
  dorm_name: string;
  room_number: string;
  booking_date: string;
}

interface AdminDataResponse {
  bookings: {
    id: number;
    student_id: string;
    booking_date: string|null;
    lease_length: number;
    dorm_name: string;
    room_number: string;
    confirmed: boolean|null;
  }[];
  maintenance_requests: MaintenanceRequestData[];
  occupied_rooms: OccupiedRoomData[];
}
