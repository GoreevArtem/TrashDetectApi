import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/app/environment";
import { JWT_NAME } from "./auth.service";

@Injectable()
export class RequestUserService {
    constructor(private http: HttpClient){}
    private path1='request/create_request';
    private path2='request/get_all_requests';
    private path3='request/get_request';
    private httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
    
    createRequest(data:any)
    {
        return this.http.post<any>(`${environment.api}${this.path1}`,data, this.httpOptions);
    }

    getRequests(limit: number)
    {
        let params = `?limit=${limit}`;
        return this.http.get<any>(`${environment.api}${this.path2}`+params, this.httpOptions);
    }

    getRequest(id: number)
    {
        let params = `?req_id=${id}`;
        return this.http.get<any>(`${environment.api}${this.path3}`+params, this.httpOptions);
    }

 
}