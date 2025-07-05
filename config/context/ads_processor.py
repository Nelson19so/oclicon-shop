from apps.products.models import Category, Product, Ad, ProductHighlight

# product active ads
def active_product_ads(request):
    context = {}

    try:
        if request.resolver_match and request.resolver_match.url_name == 'home': 
            # getting top ad for home page
            top_ad = Ad.objects.filter(is_active=True, position='top').first()

            # top right ad
            top_right_ad = Ad.objects.filter(is_active=True, position='top-right-banner').first()

            # top right bottom ad
            top_right_bottom_ad = Ad.objects.filter(
                is_active=True, position='top-right-two-banner'
            ).first()

            # featured_ad_highlight = ProductHighlight.objects.filter(features='featured_product').first()

            # featured_sidebar_ad = Ad.objects.filter(
            #     is_active=True,
            #     position='Sidebar',
            #     highlight=featured_ad_highlight,
            # ).first()

            # getting the middle banner ad
            first_middle_banner_ads = Ad.objects.filter(
                is_active=True,
                position='middle_banner'
            ).order_by('-created_at').first()

            second_middle_banner_ads = Ad.objects.filter(
                is_active=True,
                position='middle_banner'
            ).order_by('-created_at').last()

            # getting the first bottom banner ad
            first_bottom_banner = Ad.objects.filter(
                is_active=True,
                position='bottom'
            ).order_by('-created_at').first()

            filter_computer_acc_ad_ = Ad.objects.filter(
                category__name='Computer Accessories',
                position='sidebar',
                is_active=True
            ).first()

            filter_computer_acc_ad_second = Ad.objects.filter(
                category__name='Computer Accessories',
                position='sidebar',
                is_active=True
            ).last()

            context = {
                'top_ad': top_ad,
                'top_right_ad': top_right_ad,
                'top_right_bottom_ad': top_right_bottom_ad,
                'first_middle_banner_ad': first_middle_banner_ads,
                'first_bottom_banner': first_bottom_banner,
                'second_middle_banner_ads': second_middle_banner_ads,
                # 'featured_sidebar_ad': featured_sidebar_ad,
                'filter_computer_acc_ad': filter_computer_acc_ad_,
                'filter_computer_acc_ad_second': filter_computer_acc_ad_second,
            }
    except Ad.DoesNotExist:
        pass

    return context
