package com.ticketmaster.models;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;
import org.springframework.data.mongodb.core.mapping.Field;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Document(collection = "offer_range")
public class OfferRange {
    @MongoId
    private String id;

    private String name;
    private LocalDate date;

    @Field("offer_id")
    private String offerId;

    @Field("offer_range")
    private String offerRange;

    @Field("range_type")
    private String rangeType;

    @Field("created_time")
    private LocalDateTime createdTime = LocalDateTime.now();

    // Constructors
    public OfferRange() {}

    public OfferRange(String name, LocalDate date, String offerId, String offerRange) {
        this.name = name;
        this.date = date;
        this.offerId = offerId;
        this.offerRange = offerRange;
    }

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public LocalDate getDate() { return date; }
    public void setDate(LocalDate date) { this.date = date; }

    public String getOfferId() { return offerId; }
    public void setOfferId(String offerId) { this.offerId = offerId; }

    public String getOfferRange() { return offerRange; }
    public void setOfferRange(String offerRange) { this.offerRange = offerRange; }

    public String getRangeType() { return rangeType; }
    public void setRangeType(String rangeType) { this.rangeType = rangeType; }

    public LocalDateTime getCreatedTime() { return createdTime; }
    public void setCreatedTime(LocalDateTime createdTime) { this.createdTime = createdTime; }

    @Override
    public String toString() {
        return "OfferRange{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", date=" + date +
                ", offerId='" + offerId + '\'' +
                ", offerRange='" + offerRange + '\'' +
                ", rangeType='" + rangeType + '\'' +
                ", createdTime=" + createdTime +
                '}';
    }
}