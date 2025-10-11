package com.ticketmaster.models;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;
import org.springframework.data.mongodb.core.mapping.Field;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Document(collection = "price")
public class Price {
    @MongoId
    private String id;

    private String name;
    private LocalDate date;
    private String offerId;
    private String branding;

    @Field("total_price")
    private BigDecimal totalPrice;

    private String currency = "USD";

    @Field("created_time")
    private LocalDateTime createdTime = LocalDateTime.now();

    // Constructors, Getters and Setters
    public Price() {}

    public Price(String name, LocalDate date, String offerId, String branding, BigDecimal totalPrice) {
        this.name = name;
        this.date = date;
        this.offerId = offerId;
        this.branding = branding;
        this.totalPrice = totalPrice;
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

    public String getBranding() { return branding; }
    public void setBranding(String branding) { this.branding = branding; }

    public BigDecimal getTotalPrice() { return totalPrice; }
    public void setTotalPrice(BigDecimal totalPrice) { this.totalPrice = totalPrice; }

    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }

    public LocalDateTime getCreatedTime() { return createdTime; }
    public void setCreatedTime(LocalDateTime createdTime) { this.createdTime = createdTime; }
}