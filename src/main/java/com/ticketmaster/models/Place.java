package com.ticketmaster.models;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Document(collection = "place")
public class Place {
    @MongoId
    private String id;

    private String name;
    private LocalDate date;
    private String section;
    private String place;
    private String offerId;
    private LocalDateTime createdTime = LocalDateTime.now();

    // Constructors
    public Place() {}

    public Place(String name, LocalDate date, String section, String place, String offerId) {
        this.name = name;
        this.date = date;
        this.section = section;
        this.place = place;
        this.offerId = offerId;
    }

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public LocalDate getDate() { return date; }
    public void setDate(LocalDate date) { this.date = date; }

    public String getSection() { return section; }
    public void setSection(String section) { this.section = section; }

    public String getPlace() { return place; }
    public void setPlace(String place) { this.place = place; }

    public String getOfferId() { return offerId; }
    public void setOfferId(String offerId) { this.offerId = offerId; }

    public LocalDateTime getCreatedTime() { return createdTime; }
    public void setCreatedTime(LocalDateTime createdTime) { this.createdTime = createdTime; }
}