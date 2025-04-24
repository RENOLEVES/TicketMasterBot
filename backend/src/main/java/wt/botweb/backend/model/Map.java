package wt.botweb.backend.model;

import lombok.*;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
@Document(collection = "maps")
public class Map {
    @MongoId // mongodb implemented later
    private String _id;
    private List<Seat> seats;
    private String branding;
    @ToString.Exclude @EqualsAndHashCode.Exclude
    private String shape = "";

    @Data
    @AllArgsConstructor
    public static class Seat {
        private String _id;
        private String section;
        private String row;
        private String place;
        private Offer offer;
    }

    @Data
    @AllArgsConstructor
    public static class Offer {
        private String _id;
        private String min;
        private String max;
    }
}
