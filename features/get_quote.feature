Feature: Validate the test data for each lead

  Scenario: Get the lead ids, update product details and fetch quotes
    Given I load multiple lead payloads from file
    When I create lead for each reg no
    When I update product details for each lead
    When I fetch quotes for each updated lead
    Then each quote response should contain valid insurer data

