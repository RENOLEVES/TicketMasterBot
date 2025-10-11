package com.ticketmaster.repo;

import com.ticketmaster.models.Price;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

public interface PriceRepository extends MongoRepository<Price, String> {

    List<Price> findByOfferId(String offerId);

    List<Price> findByBranding(String branding);

    List<Price> findByDateAndBranding(LocalDate date, String branding);

    @Query("{ 'offerId': ?0, 'total_price': { $gte: ?1 } }")
    List<Price> findByOfferIdAndTotalPriceGreaterThanEqual(String offerId, BigDecimal minPrice);

    @Query("{ 'date': { $gte: ?0, $lte: ?1 } }")
    List<Price> findByDateBetween(LocalDate startDate, LocalDate endDate);
}