export class Card {
    public id: number;
    public adress: string;
    public request_date: string;
    public status?: string;
    public photo_name?: string;
    public class_trash?: string;
    constructor() {
        this.id=0;
        this.adress="";
        this.request_date="";
        this.status="";
     }
}