import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-Results',
  templateUrl: './Results.component.html',
  styleUrls: ['./Results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor() { }
  results: any;

  ngOnInit() {
    const resultsData = sessionStorage.getItem('results');
    this.results = resultsData ? JSON.parse(resultsData) : null;
  }
}
