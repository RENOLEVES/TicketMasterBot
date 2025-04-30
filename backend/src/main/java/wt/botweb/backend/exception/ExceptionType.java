package wt.botweb.backend.exception;

import lombok.Getter;

@Getter
public enum ExceptionType {
    ENTITY_NOT_FOUND("not found"),
    DUPLICATE_ENTITY("duplicate"),
    CUSTOM_EXCEPTION("custom");

    final String value;

    ExceptionType(String value) {
        this.value = value;
    }
}
