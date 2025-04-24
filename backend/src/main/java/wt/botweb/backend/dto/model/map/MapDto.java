package wt.botweb.backend.dto.model.map;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;
import lombok.experimental.Accessors;
import wt.botweb.backend.model.Map;

import java.util.List;

@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
@ToString
@JsonInclude(value = JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class MapDto {
    private String _id;
    private List<Map.Seat> seats;
    private String branding;
    private Map.Offer offer;
    @ToString.Exclude @EqualsAndHashCode.Exclude
    private String shape = "";
}