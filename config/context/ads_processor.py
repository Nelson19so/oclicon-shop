from apps.products.models import Category, Product, Ad, ProductHighlight

# product ads
def active_product_ads(request):
    # getting top ad for home page
    top_ad = Ad.objects.filter(is_active=True, position='top').first()

    if top_ad is None:
        pass
    
    # top right ad
    top_right_ad = Ad.objects.filter(is_active=True, position='top-right-banner').first()

    if top_right_ad is None:
        pass

    # top right bottom ad
    top_right_bottom_ad = Ad.objects.filter(
        is_active=True, position='top-right-two-banner'
    ).first()

    if top_right_bottom_ad is None:
        pass

    featured_ad_highlight = ProductHighlight.objects.filter(features='featured_product').first()

    featured_sidebar_ad = Ad.objects.filter(
        is_active=True,
        position='Sidebar',
        highlight=featured_ad_highlight,
    ).first()

    if featured_sidebar_ad is None:
        pass

    # getting the middle banner ad
    first_middle_banner_ads = Ad.objects.filter(
        is_active=True,
        position='middle_banner'
    ).order_by('-created_at').first()

    if first_middle_banner_ads is None:
        pass

    second_middle_banner_ads = Ad.objects.filter(
        is_active=True,
        position='middle_banner'
    ).order_by('-created_at').last()

    if second_middle_banner_ads is None:
        pass

    # getting the first bottom banner ad
    first_bottom_banner = Ad.objects.filter(
        is_active=True,
        position='bottom'
    ).order_by('-created_at').first()

    if first_bottom_banner is None:
        pass

    return {
        'top_ad': top_ad,
        'top_right_ad': top_right_ad,
        'top_right_bottom_ad': top_right_bottom_ad,
        'first_middle_banner_ad': first_middle_banner_ads,
        'first_bottom_banner': first_bottom_banner,
        'second_middle_banner_ads': second_middle_banner_ads,
        # 'featured_sidebar_ad': featured_sidebar_ad,
    }