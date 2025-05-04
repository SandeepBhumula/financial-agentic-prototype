package com.financialagent.cardapi.dtos;

// Using Lombok for boilerplate code reduction (getters, setters, etc.)
// Make sure Lombok is configured in your IDE
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data // Generates getters, setters, toString, equals, hashCode
@NoArgsConstructor
@AllArgsConstructor
public class CardActionRequest {
    private String cardLastFour;
    // Add other common fields if needed, or rely on specific requests
} 