# The build context is the REPOSITORY ROOT, not this directory -- see the
# `api` service in RouteOptimizer.API/docker-compose.yml. RouteOptimizer.API
# references RouteOptimizer.Infrastructure, which references
# RouteOptimizer.Core, so a context of RouteOptimizer.API alone cannot restore.

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Project files first, on their own layer: a code change then does not
# invalidate the restore, which is the slow half of this build.
COPY RouteOptimizer.sln ./
COPY RouteOptimizer.API/RouteOptimizer.API.csproj RouteOptimizer.API/
COPY RouteOptimizer.Core/RouteOptimizer.Core.csproj RouteOptimizer.Core/
COPY RouteOptimizer.Infrastructure/RouteOptimizer.Infrastructure.csproj RouteOptimizer.Infrastructure/
RUN dotnet restore RouteOptimizer.API/RouteOptimizer.API.csproj

COPY RouteOptimizer.API/ RouteOptimizer.API/
COPY RouteOptimizer.Core/ RouteOptimizer.Core/
COPY RouteOptimizer.Infrastructure/ RouteOptimizer.Infrastructure/

# All three projects use Microsoft.NET.Sdk.Web -- Core and Infrastructure are
# libraries that happen to have been created from the web template -- and that
# SDK includes appsettings*.json as content implicitly. Publishing the API
# therefore copies three appsettings.json to the same relative path and the SDK
# refuses with NETSDK1152. Only the API's configuration is ever read at runtime,
# so the libraries' copies are dropped here, which keeps the API's own
# appsettings authoritative instead of letting the SDK pick a winner.
RUN rm -f RouteOptimizer.Core/appsettings*.json \
          RouteOptimizer.Infrastructure/appsettings*.json

RUN dotnet publish RouteOptimizer.API/RouteOptimizer.API.csproj \
        -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

# curl is what the compose healthcheck calls; the aspnet image ships without it.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

COPY --from=build /app ./

# HTTP only inside the container (compose maps host 5000 -> 80). With no HTTPS
# port configured, Program.cs's UseHttpsRedirection cannot determine a target
# and lets the request through with a warning instead of answering 307.
ENV ASPNETCORE_URLS=http://+:80
EXPOSE 80

ENTRYPOINT ["dotnet", "RouteOptimizer.API.dll"]
