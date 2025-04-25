# Run a specific crawler
[group('crawler')]
crawler-run crawler season="":
    #!/usr/bin/env sh
    command="uv run footcrawl confs/{{crawler}}.yaml"
    
    if [ -n "{{season}}" ]; then
        command="$command --seasons {{season}}"
    fi
    
    eval $command


# Run multiple crawlers with multiple seasons
[group('crawler')]
crawler-many crawlers seasons="":
    #!/usr/bin/env sh
    for crawler in {{crawlers}}; do
        command="uv run footcrawl confs/$crawler.yaml"
        
        if [ -n "{{seasons}}" ]; then
            command="$command --seasons {{seasons}}"
        fi
        
        echo "Running crawler: $crawler"
        eval $command
    done