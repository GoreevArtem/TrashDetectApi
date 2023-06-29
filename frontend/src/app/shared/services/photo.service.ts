import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders} from "@angular/common/http";
import { GlobalConfig } from "src/app/global";
import { environment } from "src/app/environment";

@Injectable()
export class PhotoService {
    constructor(private http: HttpClient){}
    private path1='request/detection';
    private path2='request/filepath';

    uploadPhoto(data:any)
    {
        var headers_object = new HttpHeaders().set("Authorization", "Bearer " + GlobalConfig.t);
        const httpOptions = {
            headers: headers_object
        };
        return this.http.post(`${environment.api}${this.path1}`,data, httpOptions);
    }

    downloadPhoto(file_name:any)
    {
        let params = `?upload_name=${file_name}`;
        var headers_object = new HttpHeaders().set("Authorization", "Bearer " + GlobalConfig.t);
        return this.http.get(`${environment.api}${this.path2}`+params,{headers: headers_object, responseType:'blob'});
    }
}