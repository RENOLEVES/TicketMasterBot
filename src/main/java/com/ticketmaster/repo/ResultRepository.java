package com.ticketmaster.repo;

import com.ticketmaster.models.Result;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.time.LocalDateTime;
import java.util.List;

import java.math.BigDecimal;


public interface ResultRepository extends MongoRepository<Result, String> {

    List<Result> findByOfferId(String offerId);

    List<Result> findByBranding(String branding);

    List<Result> findByStatus(Result.ResultStatus status);

    List<Result> findByBrandingAndStatus(String branding, Result.ResultStatus status);

    @Query("{ 'calculated_at': { $gte: ?0 } }")
    List<Result> findByCalculatedAtAfter(LocalDateTime dateTime);

    @Query("{ 'calculated_at': { $gte: ?0, $lte: ?1 } }")
    List<Result> findByCalculatedAtBetween(LocalDateTime start, LocalDateTime end);

    @Query("{ 'price': { $gte: ?0 } }")
    List<Result> findByPriceGreaterThanEqual(BigDecimal minPrice);

    @Query("{ 'offer_id': ?0, 'result_type': ?1 }")
    List<Result> findByOfferIdAndResultType(String offerId, String resultType);

    @Query(value = "{ 'offer_id': ?0 }", delete = true)
    long deleteAllByOfferId(String offerId);

    @Query(value = "{ 'offer_id': ?0 }", exists = true)
    boolean existsByOfferId(String offerId);
}