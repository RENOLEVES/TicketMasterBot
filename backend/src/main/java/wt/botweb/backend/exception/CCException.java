package wt.botweb.backend.exception;

public class CCException extends RuntimeException{
    public CCException(String message){
        super(message);
    }

    public static RuntimeException throwException(EntityType entityType, ExceptionType exceptionType, String... args) {
        String message = String.format("%s %s with ID %s", entityType, exceptionType, args[0]);
        return new CCException(message);
    }
}
