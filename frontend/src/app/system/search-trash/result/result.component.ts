import { Component } from '@angular/core';
import { GlobalConfig } from 'src/app/global';
import { PhotoService } from 'src/app/shared/services/photo.service';
import { YandexMapService } from '../../../shared/services/yandex-map_service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {
  sentAdress=GlobalConfig.adress;
  file = localStorage.getItem('path');
  image_src:any;
  base64data:any;
  isOpen = false;

  open() {
    this.isOpen = !this.isOpen;
  }

  isOpen2 = false;
  open2() {
    this.isOpen2 = !this.isOpen2;
  }

  constructor(private yandexMap: YandexMapService, private photoService:PhotoService) { }
  ngOnInit(): void {
  this.yandexMap.initMap(56.323163, 43.866262);
  this.photoService.downloadPhoto(encodeURIComponent(""+this.file))
  .subscribe((blob:any)=>{
    this.image_src=window.URL.createObjectURL(blob);
  })
  }
}

