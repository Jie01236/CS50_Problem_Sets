-- Keep a log of any SQL queries you execute as you solve the mystery.

-- find in crime_scene_reports
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND
 day = 28 AND street = 'Humphrey Street';
 -- find in interviews
 SELECT transcript
 FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- find in bakery
SELECT license_plate, activity
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >=15 AND minute <= 25;

-- match the license plate with people table (8 persons)
SELECT DISTINCT name
FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >=15 AND minute <= 25;

-- find in atm informations
SELECT account_number
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- match bank account and people id (8 persons)
SELECT name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- find in phone_calls
SELECT receiver, caller
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- match phone number with people (9 person)
SELECT caller_name.name AS caller_name, receiver_name.name AS receiver_name, phone_calls.caller, phone_calls.receiver
FROM phone_calls
JOIN people AS caller_name ON phone_calls.caller = caller_name.phone_number
JOIN people AS receiver_name ON phone_calls.receiver = receiver_name.phone_number
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--find in flight
SELECT id, origin_airport_id, destination_airport_id, hour, minute
FROM flights
WHERE year = 2021 AND month = 7 AND day = 29
ORDER BY hour ASC
LIMIT 1;

--match with airport
SELECT flights.destination_airport_id, airports.city AS destination_city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE flights.origin_airport_id = 8 AND flights.hour = 8 AND flights.minute = 20;

-- find in passengers (8 persons)
SELECT name, phone_number, license_plate from people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE flights.id = 36;

-- put all together
SELECT name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE (flights.origin_airport_id = 8 AND flights.hour = 8 AND flights.minute = 20 AND flights.id = 36)
AND name IN(
    SELECT name
    FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND name IN(
    SELECT DISTINCT name
    FROM people
    JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >=15 AND minute <= 25)
AND name IN(
    SELECT caller_name.name
    FROM phone_calls
    JOIN people AS caller_name ON phone_calls.caller = caller_name.phone_number
    JOIN people AS receiver_name ON phone_calls.receiver = receiver_name.phone_number
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60);
