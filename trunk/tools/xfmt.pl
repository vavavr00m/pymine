#!/usr/bin/perl
while (<>) {
    ($class, $http, $url, $method, @rest) = split;
    printf("%-6s %-6s %-30s %s @rest\n", $class, $http, $url, $method)
}
