package com.ticketmaster.repo;

import com.ticketmaster.models.OfferRange;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

public interface OfferRangeRepository extends MongoRepository<OfferRange, String> {

    List<OfferRange> findByOfferId(String offerId);

    List<OfferRange> findByDate(LocalDate date);

    List<OfferRange> findByNameContaining(String name);

    @Query("{ 'offer_range': { $regex: ?0, $options: 'i' } }")
    List<OfferRange> findByOfferRangeRegex(String rangePattern);

    @Query("{ 'offer_id': ?0, 'range_type': ?1 }")
    List<OfferRange> findByOfferIdAndRangeType(String offerId, String rangeType);

    boolean existsByOfferId(String offerId);

    long deleteByOfferId(String offerId);

    Optional<OfferRange> findFirstByOfferIdOrderByCreatedTimeDesc(String offerId);
}