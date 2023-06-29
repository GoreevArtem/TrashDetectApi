import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/app/environment";
import { JWT_NAME } from "./auth.service";

@Injectable()
export class ExpertService {
    constructor(private http: HttpClient){}
    private path1='expert/me';
    private path2='expert/me_update';

    getExpert()
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.get<any>(`${environment.api}${this.path1}`,httpOptions);
    }

    updatePassword(data:any)
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.patch(`${environment.api}${this.path2}`,data,httpOptions);
    }
}