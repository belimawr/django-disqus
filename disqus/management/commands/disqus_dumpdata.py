from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
import json

from disqusapi import DisqusAPI, APIError, Paginator


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--indent', default=None, dest='indent', type='int',
            help='Specifies the indent level to use when pretty-printing output'),
        make_option('--filter', default='', dest='filter', type='str',
            help='Type of entries that should be returned'),
        make_option('--exclude', default='', dest='exclude', type='str',
            help='Type of entries that should be excluded from the response'),
    )
    help = 'Output DISQUS data in JSON format'
    requires_model_validation = False

    def handle(self, **options):
        from django.conf import settings

        client = DisqusAPI(settings.DISQUS_SECRET_KEY, settings.DISQUS_PUBLIC_KEY)
        indent = options.get('indent')
        filter_ = options.get('filter')
        exclude = options.get('exclude')

        default_filter = ['approved']
        default_exclude = ['unapproved', 'spam', 'deleted', 'flagged', 'highlighted']

        if exclude:
            final_filter = set(default_filter + default_exclude).difference(exclude)
        else:
            final_filter = filter_ if filter_ else default_filter

        # Get a list of all forums for an API key. Each API key can have 
        # multiple forums associated. This application only supports the one 
        # set in the DISQUS_WEBSITE_SHORTNAME variable
        try:
            threads = client.forums.listThreads(forum=settings.DISQUS_WEBSITE_SHORTNAME)
        except APIError:
            raise CommandError("Could not find forum. " +
                               "Please check your " +
                               "'DISQUS_WEBSITE_SHORTNAME' setting.")

        posts_paginator = Paginator(client.posts.list, forum='omeletebr', related=['thread'], include=final_filter) # since=last_month
        posts = list(posts_paginator)

        print json.dumps(posts, indent=indent)
