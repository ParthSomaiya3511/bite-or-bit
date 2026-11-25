from django.urls import path

from .views import (
    create_order,
    order_history,
    create_payment,
    verify_payment,
    generate_invoice,
    user_orders,
    AdminOrdersView,
    UpdateOrderStatusView,
    TrackOrderView,
    CreatePaymentView,
    VerifyPaymentView,
    SingleOrderView,
    UpdateDeliveryLocation,
    GetDeliveryLocation,
    DeliveryETAView,
    UpdateDeliveryLocationView,
    DeliveryBoySimulationView,
    UpdateRiderLocationView,
    RiderLoginAPIView,
    RiderDashboardView,
    RiderOrdersView,
    UpdateRiderGPSAPIView,
    AcceptOrderAPIView,
    SendChatMessageAPIView,
    OrderChatAPIView,
    RiderStatsView,
    CompleteDeliveryAPIView,
    CreateOrderView,
    AllOrdersView,
    ClusterOrdersView,
    SmartPriorityView,
    AutoAssignRiderView,
    DeliveryHeatmapView,
    OrderBatchView,
    PredictiveDemandView,
    RiderAnalyticsView,
    FraudOrdersView,
    CreateWithdrawView,
    RiderLeaderboardView,
    RiderAchievementView,
    RiderMissionView,
    RiderStreakView,
    RiderDisciplineView,
    RiderClockInView,
    RiderClockOutView,
    RiderShiftAnalyticsView,
    GenerateRiderScheduleView,
    BestScheduledRiderView,
    RiderMoodAPIView,
    RiderSafetyAPIView,
    CreateSOSView,
    ResolveSOSView,
    VoiceSOSView,
    DeliveryHeatmapView,
    RestaurantRegisterView,
    RestaurantLoginView,
    RestaurantDashboardView,
    AddFoodView,
    RestaurantFoodListView,
    UpdateFoodView,
    DeleteFoodView,
    CreateWalletView,
    AddMoneyView,
    WalletBalanceView,
    WalletHistoryView,
    WalletPaymentView,
    WalletRefundView,
    CreateRazorpayOrderView,
    VerifyRazorpayPaymentView,
    CreateStripePaymentView,
    CreateMembershipPlanView,
    PurchaseMembershipView,
    CheckMembershipView,
    CreateCouponView,
    ApplyCouponView,
    ApplyReferralCodeView,
    ReferralHistoryView,
    RewardDashboardView,
    AIRecommendationView,
    CustomerAnalyticsView,
    SaveFCMTokenView,
    AdminAnalyticsView,
    CustomerNotificationView,
    MarkNotificationReadView,
    CustomerOrderHistoryView,
    CustomerOrderDetailView,
    CustomerProfileView,
    UpdateCustomerProfileView,
    AddCustomerAddressView,
    CustomerAddressListView,
    UpdateCustomerAddressView,
    DeleteCustomerAddressView,
    CreateSupportTicketView,
    CustomerSupportTicketsView,
    SupportTicketDetailView,
    AddSupportMessageView,
    SubmitFeedbackView,
    CustomerFeedbackHistoryView,
    RestaurantRatingAnalyticsView,
    RiderRatingAnalyticsView,

)

urlpatterns = [

    path(
        "orders/",
        create_order
    ),

    path('history/', order_history),

    path('payment/', create_payment),

    path('verify-payment/', verify_payment),

    path('invoice/<int:order_id>/', generate_invoice),
    
    path("my-orders/", user_orders),
    
    path(
        "admin-orders/",
        AdminOrdersView.as_view()
    ),

    path(
        "<int:id>/update-status/",
        UpdateOrderStatusView.as_view()
    ),
    
    path(
        "create-payment/",
        CreatePaymentView.as_view()
    ),

    path(
        "verify-payment/",
        VerifyPaymentView.as_view()
    ),
    
    path(
        "<int:id>/",
        SingleOrderView.as_view()
    ),
    
    path(
        "admin-orders/",
        AdminOrdersView.as_view()
    ),

    path(
        "update-status/<int:id>/",
        UpdateOrderStatusView.as_view()
    ),
    
    path(
        "delivery-location/",
        UpdateDeliveryLocation.as_view()
    ),

    path(
        "delivery-location/<int:order_id>/",
        GetDeliveryLocation.as_view()
    ),
    
    path(
        "eta/<int:id>/",
        DeliveryETAView.as_view()
    ),
    
    path(
        "update-location/<int:id>/",
        UpdateDeliveryLocationView.as_view()
    ),
    
    path(
        "simulate-rider/<int:id>/",
        DeliveryBoySimulationView.as_view()
    ),
    
    path(
        "update-rider-location/",
        UpdateRiderLocationView.as_view()
    ),
    
    # RIDER LOGIN
    path( 
        "rider-login/", 
        RiderLoginAPIView.as_view() 
    ),

    # RIDER DASHBOARD
    path(
        "rider/dashboard/<int:rider_id>/",
        RiderDashboardView.as_view()
    ), 

    # RIDER ORDERS
    path(
        "rider/orders/<int:rider_id>/",
        RiderOrdersView.as_view()
    ),

    # UPDATE GPS
    path(
        "update-rider-gps/<int:order_id>/",
        UpdateRiderGPSAPIView.as_view()
    ),
    
    path( 
        "accept-order/<int:order_id>/", 
        AcceptOrderAPIView.as_view() 
    ),

    path(
        "chat/send/",
        SendChatMessageAPIView.as_view()
    ),

    path(
        "chat/<int:order_id>/",
        OrderChatAPIView.as_view()
    ),
    
    # RIDER STATS

    path(
        "rider-stats/<int:rider_id>/",
        RiderStatsView.as_view()
    ),

    # COMPLETE DELIVERY

    path(
        "complete-order/<int:order_id>/",
        CompleteDeliveryAPIView.as_view()
    ),
    
    path( 
        "create-order/", 
        CreateOrderView.as_view() 
    ), 
    
    path( 
        "track-order/<int:id>/", 
        TrackOrderView.as_view() 
    ), 
    
    path( 
        "all-orders/", 
        AllOrdersView.as_view() 
    ), 
    
    path(
        'cluster-orders/',
        ClusterOrdersView.as_view()
    ),
    
    path(
        'smart-priority/',
        SmartPriorityView.as_view()
    ),
    
    path(
        'auto-assign/<int:id>/',
        AutoAssignRiderView.as_view()
    ),
    
    path(
        'delivery-heatmap/',
        DeliveryHeatmapView.as_view()
    ),

    path(
        'order-batches/',
        OrderBatchView.as_view()
    ),
    
    path(
        'predict-demand/',
        PredictiveDemandView.as_view()
    ),
    
    path(
        'rider-analytics/',
        RiderAnalyticsView.as_view()
    ),
    
    path(
        'fraud-orders/',
        FraudOrdersView.as_view()
    ),
    
    path(
        "withdraw/create/",
        CreateWithdrawView.as_view()
    ),
    
    path(
        "leaderboard/",
        RiderLeaderboardView.as_view()
    ),
    
    path(
        "rider-achievements/<int:rider_id>/",
        RiderAchievementView.as_view()
    ),

    path(
        "rider-missions/<int:rider_id>/",
        RiderMissionView.as_view()
    ),
    
    path(
        "rider-streak/<int:rider_id>/",
        RiderStreakView.as_view()
    ),
    
    path(
        "rider-discipline/<int:rider_id>/",
        RiderDisciplineView.as_view()
    ),
    
    path(
        "rider-clock-in/<int:rider_id>/",
        RiderClockInView.as_view()
    ),

    path(
        "rider-clock-out/<int:rider_id>/",
        RiderClockOutView.as_view()
    ),

    path(

        "rider-shift-analytics/<int:rider_id>/",
        RiderShiftAnalyticsView.as_view()
    ),
    
    path(
        "generate-rider-schedule/<int:rider_id>/",
        GenerateRiderScheduleView.as_view()
    ),

    path(
        "best-scheduled-rider/",
        BestScheduledRiderView.as_view()
    ),
    
    path(
        'rider-mood/<int:rider_id>/',
        RiderMoodAPIView.as_view()
    ),
    
    path(
        'rider-safety/',
        RiderSafetyAPIView.as_view()
    ),
    
    path(
        'create-sos/',
        CreateSOSView.as_view()
    ),

    path(
        'resolve-sos/<int:id>/',
        ResolveSOSView.as_view()
    ),
    
    path(
        "sos/voice-sos/", 
        VoiceSOSView.as_view()
    ),
    
    path(
        'delivery-heatmap/',
        DeliveryHeatmapView.as_view()
    ),
    
    path(
        'restaurant-register/',
        RestaurantRegisterView.as_view()
    ),
    
    path(

        'restaurant-login/',
        RestaurantLoginView.as_view()
    ),
    
    path(
        'restaurant-dashboard/<int:restaurant_id>/',
        RestaurantDashboardView.as_view()
    ),
    
    path(

        'add-food/',
        AddFoodView.as_view()
    ),

    path(

        'restaurant-foods/<int:restaurant_id>/',
        RestaurantFoodListView.as_view()
    ),

    path(

        'update-food/<int:food_id>/',
        UpdateFoodView.as_view()
    ),

    path(

        'delete-food/<int:food_id>/',
        DeleteFoodView.as_view()
    ),
    
    path(
        'create-wallet/',
        CreateWalletView.as_view()
    ),

    path(
        'add-money/',
        AddMoneyView.as_view()
    ),

    path(
        'wallet-balance/<str:mobile>/',
        WalletBalanceView.as_view()
    ),

    path(
        'wallet-history/<str:mobile>/',
        WalletHistoryView.as_view()
    ),
    
    path(
        'wallet-payment/',
        WalletPaymentView.as_view()
    ),

    path(
        'wallet-refund/',
        WalletRefundView.as_view()
    ),
    
    path(
        'create-razorpay-order/',
        CreateRazorpayOrderView.as_view()
    ),

    path(
        'verify-razorpay-payment/',
        VerifyRazorpayPaymentView.as_view()
    ),

    path(
        'create-stripe-payment/',
        CreateStripePaymentView.as_view()
    ),
    
    path(
        'create-membership-plan/',
        CreateMembershipPlanView.as_view()
    ),

    path(
        'purchase-membership/',
        PurchaseMembershipView.as_view()
    ),

    path(
        'check-membership/<str:mobile>/',
        CheckMembershipView.as_view()
    ),
    
    path(
        'create-coupon/',
        CreateCouponView.as_view()
    ),

    path(
        'apply-coupon/',
        ApplyCouponView.as_view()
    ),
    
    path(
        'apply-referral/',
        ApplyReferralCodeView.as_view()
    ),

    path(
        'referral-history/<str:mobile>/',
        ReferralHistoryView.as_view()
    ),

    path(
        'reward-dashboard/<str:mobile>/',
        RewardDashboardView.as_view()
    ),
    
    path(
        'ai-recommendations/<str:mobile>/',
        AIRecommendationView.as_view()
    ),
    
    path(
        'customer-analytics/',
        CustomerAnalyticsView.as_view()
    ),
    
    path(
        'save-fcm-token/',
        SaveFCMTokenView.as_view()
    ),
    
    path(
        'admin-analytics/',
        AdminAnalyticsView.as_view()
    ),
    
    path(
        'notifications/',
        CustomerNotificationView.as_view()
    ),

    path(
        'notification-read/',
        MarkNotificationReadView.as_view()
    ),
    
    path(
        'customer-order-history/',
        CustomerOrderHistoryView.as_view()
    ),

    path(
        'customer-order-detail/<int:id>/',
        CustomerOrderDetailView.as_view()
    ),
    
    path(
        'customer-profile/',
        CustomerProfileView.as_view()
    ),

    path(
        'update-customer-profile/',
        UpdateCustomerProfileView.as_view()
    ),
    
    path(
        'add-address/',
        AddCustomerAddressView.as_view()
    ),

    path(
        'address-list/',
        CustomerAddressListView.as_view()
    ),

    path(
        'update-address/',
        UpdateCustomerAddressView.as_view()
    ),

    path(
        'delete-address/',
        DeleteCustomerAddressView.as_view()
    ),
    
    path(
        'create-ticket/',
        CreateSupportTicketView.as_view()
    ),

    path(
        'customer-tickets/',
        CustomerSupportTicketsView.as_view()
    ),

    path(
        'ticket-detail/<int:id>/',
        SupportTicketDetailView.as_view()
    ),

    path(
        'add-ticket-message/',
        AddSupportMessageView.as_view()
    ),
    
    path(
        'submit-feedback/',
        SubmitFeedbackView.as_view()
    ),

    path(
        'feedback-history/',
        CustomerFeedbackHistoryView.as_view()
    ),

    path(
        'restaurant-ratings/<int:id>/',
        RestaurantRatingAnalyticsView.as_view()
    ),

    path(
        'rider-ratings/<int:id>/',
        RiderRatingAnalyticsView.as_view()
    ),



]