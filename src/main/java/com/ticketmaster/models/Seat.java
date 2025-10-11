package com.ticketmaster.models;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;
import org.springframework.data.mongodb.core.mapping.Field;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Document(collection = "seat")
public class Seat {
    @MongoId
    private String id;

    private String name;
    private LocalDate date;
    private BigDecimal price;
    private String description;
    private String section;
    private String row;
    private String branding;

    @Field("offer_id")
    private String offerId;

    private SeatStatus status = SeatStatus.AVAILABLE;

    @Field("created_time")
    private LocalDateTime createdTime = LocalDateTime.now();

    // Enum for seat status
    public enum SeatStatus {
        AVAILABLE, RESERVED, SOLD
    }

    // Constructors
    public Seat() {}

    public Seat(String name, LocalDate date, BigDecimal price, String section, String row, String offerId) {
        this.name = name;
        this.date = date;
        this.price = price;
        this.section = section;
        this.row = row;
        this.offerId = offerId;
    }

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public LocalDate getDate() { return date; }
    public void setDate(LocalDate date) { this.date = date; }

    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getSection() { return section; }
    public void setSection(String section) { this.section = section; }

    public String getRow() { return row; }
    public void setRow(String row) { this.row = row; }

    public String getBranding() { return branding; }
    public void setBranding(String branding) { this.branding = branding; }

    public String getOfferId() { return offerId; }
    public void setOfferId(String offerId) { this.offerId = offerId; }

    public SeatStatus getStatus() { return status; }
    public void setStatus(SeatStatus status) { this.status = status; }

    public LocalDateTime getCreatedTime() { return createdTime; }
    public void setCreatedTime(LocalDateTime createdTime) { this.createdTime = createdTime; }

    @Override
    public String toString() {
        return "Seat{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", date=" + date +
                ", price=" + price +
                ", section='" + section + '\'' +
                ", row='" + row + '\'' +
                ", branding='" + branding + '\'' +
                ", offerId='" + offerId + '\'' +
                ", status=" + status +
                ", createdTime=" + createdTime +
                '}';
    }
}