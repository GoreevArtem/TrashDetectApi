import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LocalStorageService {

  coords: Array<any> = [];
  key: string = "coords"

  constructor() {}

  getAllLocalStorage() {
    this.coords = JSON.parse(localStorage.getItem(this.key) as string) || [];
  }

  addItem(item: any) {
    this.coords.push(item)
    localStorage.setItem(this.key, JSON.stringify(this.coords))
  }

  removeItem(item: any) {
    this.coords = this.coords.filter(el => el !== item);
    localStorage.setItem(this.key, JSON.stringify(this.coords))
  }

}