import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [],
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

  ngOnInit(): void {
    // Initialize component data here

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