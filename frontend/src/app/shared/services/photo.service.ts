import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders} from "@angular/common/http";
import { GlobalConfig } from "src/app/global";
import { environment } from "src/app/environment";
import { JWT_NAME } from "./auth.service";

@Injectable()
export class PhotoService {
    constructor(private http: HttpClient){}
    private path1='request/detection';
    private path2='request/filepath';
    private path3='expert/get_photo';
   
    uploadPhoto(data:any)
    {
        var headers_object = new HttpHeaders().set("Authorization", "Bearer " + localStorage.getItem(JWT_NAME));
        const httpOptions = {
            headers: headers_object
        };
        return this.http.post(`${environment.api}${this.path1}`,data, httpOptions);
    }

    downloadPhoto(file_name:any)
    {
        let params = `?upload_name=${file_name}`;
        var headers_object = new HttpHeaders().set("Authorization", "Bearer " + localStorage.getItem(JWT_NAME));
        return this.http.get(`${environment.api}${this.path2}`+params,{headers: headers_object, responseType:'blob'});
    }

    downloadPhotoEx(id:any)
    {
        let params = `?req_id=${id}`;
        var headers_object = new HttpHeaders().set("Authorization", "Bearer " + localStorage.getItem(JWT_NAME));
      
        return this.http.get(`${environment.api}${this.path3}`+params,{headers: headers_object, responseType:'blob'});
    }
    
}