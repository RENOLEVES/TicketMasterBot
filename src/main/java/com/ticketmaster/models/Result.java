package com.ticketmaster.models;

import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;
import org.springframework.data.mongodb.core.mapping.Field;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Document(collection = "result")
public class Result {
    @MongoId
    private String id;

    private BigDecimal price;
    private String description;
    private String branding;

    @Field("offer_id")
    private String offerId;

    @Field("result_type")
    private String resultType;

    @Field("calculated_at")
    private LocalDateTime calculatedAt = LocalDateTime.now();

    private ResultStatus status = ResultStatus.SUCCESS;

    // Constructors
    public Result() {}

    public Result(BigDecimal price, String branding, String offerId) {
        this.price = price;
        this.branding = branding;
        this.offerId = offerId;
    }

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getBranding() { return branding; }
    public void setBranding(String branding) { this.branding = branding; }

    public String getOfferId() { return offerId; }
    public void setOfferId(String offerId) { this.offerId = offerId; }

    public String getResultType() { return resultType; }
    public void setResultType(String resultType) { this.resultType = resultType; }

    public LocalDateTime getCalculatedAt() { return calculatedAt; }
    public void setCalculatedAt(LocalDateTime calculatedAt) { this.calculatedAt = calculatedAt; }

    public ResultStatus getStatus() { return status; }
    public void setStatus(ResultStatus status) { this.status = status; }

    @Override
    public String toString() {
        return "Result{" +
                "id='" + id + '\'' +
                ", price=" + price +
                ", branding='" + branding + '\'' +
                ", offerId='" + offerId + '\'' +
                ", resultType='" + resultType + '\'' +
                ", calculatedAt=" + calculatedAt +
                ", status=" + status +
                '}';
    }
}