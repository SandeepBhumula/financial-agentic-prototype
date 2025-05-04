-- Create the Card table within the cards schema
CREATE TABLE IF NOT EXISTS cards.card (
    id BIGSERIAL PRIMARY KEY,                            -- Unique identifier for the card record
    card_number_hash VARCHAR(255) NOT NULL UNIQUE,       -- Secure hash of the full card number (PAN)
    last_four_digits VARCHAR(4) NOT NULL,                -- Last four digits of the card number for display/identification
    cardholder_name VARCHAR(255) NULL,                   -- Name of the cardholder (Can be NULL initially if not known)
    expiry_date DATE NOT NULL,                           -- Card expiration date (YYYY-MM-DD format)
    status VARCHAR(20) NOT NULL                          -- Card status (e.g., 'PRE_ACTIVATED', 'ACTIVE', 'DEACTIVATED', 'EXPIRED', 'LOST', 'STOLEN')
        CHECK (status IN ('PRE_ACTIVATED', 'ACTIVE', 'DEACTIVATED', 'EXPIRED', 'LOST', 'STOLEN')),
    customer_id VARCHAR(100) NOT NULL,                   -- Identifier linking the card to a customer record
    activation_date TIMESTAMP WITH TIME ZONE NULL,       -- Timestamp when the card was activated
    deactivation_date TIMESTAMP WITH TIME ZONE NULL,     -- Timestamp when the card was deactivated
    deactivation_reason VARCHAR(255) NULL,               -- Reason for deactivation (if applicable)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the record was created
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Timestamp when the record was last updated
);

-- Index on status for common lookups
CREATE INDEX IF NOT EXISTS idx_card_status ON cards.card(status);

-- Index for finding cards by last four digits and customer ID (common lookup scenario)
CREATE UNIQUE INDEX IF NOT EXISTS idx_card_lastfour_customerid ON cards.card(last_four_digits, customer_id);

-- Index for finding a card by its hash (essential for lookup)
CREATE UNIQUE INDEX IF NOT EXISTS idx_card_numberhash ON cards.card(card_number_hash);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION cards.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at timestamp on update
DROP TRIGGER IF EXISTS trg_card_update_timestamp ON cards.card;

CREATE TRIGGER trg_card_update_timestamp
BEFORE UPDATE ON cards.card
FOR EACH ROW
EXECUTE FUNCTION cards.update_updated_at_column(); 