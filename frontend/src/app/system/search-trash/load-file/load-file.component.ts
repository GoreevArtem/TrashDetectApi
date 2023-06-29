import { Component, ChangeDetectorRef } from '@angular/core';
import { PhotoService } from 'src/app/shared/services/photo.service';
import { HttpClient } from '@angular/common/http';
import { FormBuilder } from '@angular/forms';
import { GlobalConfig } from 'src/app/global';
import { HttpHeaders } from '@angular/common/http';
import { formatDate } from '@angular/common';
import { environment } from 'src/app/environment';

@Component({
  selector: 'app-load-file',
  templateUrl: './load-file.component.html',
  styleUrls: ['./load-file.component.css']
})
export class LoadFileComponent {
  imageUploaded = false;
  documentUploaded = false;
  hintIsShowed = true;
  imgName:any;
  myFiles: string[] = [];
  files:any=[];
  reader=new FileReader();
  file:any;
  filename:any = "";
  

  next=false;

  constructor(private photoService: PhotoService, public fb: FormBuilder, private change: ChangeDetectorRef) { }
  
  getFileDetails(e: any) {
    for (var i = 0; i < e.target.files.length; i++) {
      let file = e.target.files[0];
      let reader = new FileReader();
      reader.readAsText(file);
      this.file = reader.result;
      this.myFiles.push(e.target.files[i]);
      this.files.push(e.target.files[i]);
      this.change.detectChanges();
    }
    var file:any;
    const frmData = new FormData();
      frmData.append("file", this.myFiles[0]);
    this.files[0].text().then((res:any) => {file = res})
    .then(() => {
      this.photoService.uploadPhoto(frmData)
      .subscribe(
        (value:any) => {
          console.log(value);
          this.imgName = value.name_photo;
          GlobalConfig.path=value.name_photo;
          this.imageUploaded = true;
          this.next=true;
        },
      )
    });
    this.myFiles = [];
  }

  getFileBinary(file:any):any{
      let res;
      file.text().then(function (text:any) {
        res = text;
      });
      return res;
  }
 }
