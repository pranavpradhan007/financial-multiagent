import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple, List
import random

def load_financial_phrasebank(file_path: str = "data/dataset/all-data.csv") -> Tuple[List[str], List[str], List[int], List[int]]:
    """
    Load and preprocess the Financial PhraseBank dataset.

    Args:
        file_path (str): Path to the CSV file containing the dataset.

    Returns:
        Tuple containing:
        - train_texts: List of training sentences
        - test_texts: List of test sentences
        - train_labels: List of training labels
        - test_labels: List of test labels
    """
    try:
        df = pd.read_csv(file_path)
        
        if 'sentence' not in df.columns or 'label' not in df.columns:
            raise ValueError("CSV file must contain 'sentence' and 'label' columns")
        
        label_map = {"positive": 2, "neutral": 1, "negative": 0}
        df['label'] = df['label'].map(label_map)
        
        train_texts, test_texts, train_labels, test_labels = train_test_split(
            df['sentence'].tolist(),
            df['label'].tolist(),
            test_size=0.2,
            random_state=42,
            stratify=df['label']
        )
        
        return train_texts, test_texts, train_labels, test_labels
    
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found. Please check the path and try again.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the dataset: {str(e)}")
    

    

def load_mock_headlines(ticker, count=50):
    """
    Load a balanced set of mock headlines (positive, neutral, negative) for testing.
    Provides at least 50 unique-ish headlines per major tech ticker.

    Args:
        ticker (str): The stock ticker symbol (e.g., "TSLA", "AAPL").
        count (int): The maximum number of headlines to return.

    Returns:
        list[str]: A list of mock headlines for the given ticker.
    """

    # --- Headline Templates ---

    positive_templates = [
        # Earnings & Financials
        "{ticker} posts record quarterly revenue, smashing estimates",
        "{ticker} beats EPS expectations by {percent}%, stock jumps",
        "Strong profit margins reported by {ticker} in latest quarter",
        "{ticker} raises full-year guidance after strong performance",
        "Impressive free cash flow generation highlighted in {ticker}'s earnings call",
        "{ticker} announces increased stock buyback program",
        "Dividend hike declared by {ticker}, rewarding shareholders",
        "Positive analyst revisions follow {ticker}'s solid earnings report",
        "{ticker} demonstrates significant debt reduction progress",
        "Financial health of {ticker} rated 'Excellent' by Moody's/S&P",

        # Product & Innovation
        "{ticker} unveils breakthrough {product_type} technology, potential game-changer",
        "Successful launch of new {ticker} {product_name} sees high demand",
        "Rave reviews for {ticker}'s latest {product_or_service}",
        "{ticker}'s R&D pipeline shows promising developments in {area}",
        "Innovation award granted to {ticker} for {specific_achievement}",
        "Early adoption rates for {ticker}'s new platform exceed forecasts",
        "{ticker} expands {service_name} offering to new markets",
        "Patent granted to {ticker} for novel {technology_field} invention",
        "User interface improvements rolled out for {ticker}'s core product",
        "{ticker} demonstrates leadership in sustainable technology practices",

        # Market Position & Growth
        "{ticker} gains market share from competitors in {key_segment}",
        "Analyst upgrades {ticker} to 'Strong Buy' citing growth potential",
        "{ticker} stock hits new 52-week high on positive momentum",
        "Strategic acquisition of {acquired_company} set to boost {ticker}'s growth",
        "Major partnership announced between {ticker} and {partner_company}",
        "{ticker} expands operations into the lucrative {region} market",
        "Strong user/customer growth reported by {ticker}",
        "Network effect strengthens {ticker}'s competitive moat",
        "{ticker} rated as 'Top Pick' in the tech sector by {investment_bank}",
        "Customer satisfaction scores for {ticker} reach all-time high",

        # Management & Strategy
        "Visionary leadership praised at {ticker}'s investor day",
        "Effective cost management strategies implemented by {ticker}",
        "{ticker} successfully navigates supply chain challenges",
        "Smooth CEO transition ensures continuity at {ticker}",
        "Corporate social responsibility initiatives from {ticker} well-received",
    ]

    negative_templates = [
        # Earnings & Financials
        "{ticker} misses quarterly revenue targets, stock tumbles",
        "{ticker} reports unexpected loss, shocking analysts",
        "Declining profit margins raise concerns for {ticker}",
        "{ticker} lowers guidance citing macroeconomic headwinds",
        "Cash burn rate increases at {ticker}, worries investors",
        "{ticker} suspends dividend payments amid financial uncertainty",
        "Analyst downgrades {ticker} to 'Sell' due to poor outlook",
        "Rising costs pressure {ticker}'s bottom line",
        "{ticker}'s debt levels reach concerning heights",
        "Credit rating agency issues negative outlook for {ticker}",

        # Product & Innovation
        "Launch of {ticker}'s new {product_name} plagued by technical glitches",
        "Poor reviews and customer complaints hit {ticker}'s {product_or_service}",
        "{ticker}'s {product_type} deemed 'underwhelming' by critics",
        "Delays announced for highly anticipated {ticker} product release",
        "{ticker} faces criticism over lack of innovation in recent years",
        "{ticker} issues recall for faulty {product_component}",
        "Security vulnerability discovered in {ticker}'s {platform_name} software",
        "Key R&D project cancelled at {ticker} after setbacks",
        "Competitor unveils superior technology, challenging {ticker}",
        "Ethical concerns raised over {ticker}'s use of {technology_area}",

        # Market Position & Growth
        "{ticker} loses market share to aggressive new entrant {competitor}",
        "Antitrust probe launched into {ticker}'s business practices in {region}",
        "{ticker} stock price drops significantly below moving averages",
        "Failed acquisition attempt costs {ticker} millions",
        "Regulatory hurdles block {ticker}'s expansion plans",
        "User growth stagnates for {ticker}'s core platform",
        "Class-action lawsuit filed against {ticker} regarding {issue}",
        "Intensifying competition in katon pressures {ticker}",
        "Supply chain disruptions severely impact {ticker}'s output",
        "Negative publicity damages {ticker}'s brand reputation",

        # Management & Strategy
        "Sudden departure of key executive [{exec_name}] raises questions at {ticker}",
        "Strategic missteps lead to write-downs for {ticker}",
        "{ticker} management criticized for poor capital allocation",
        "Reports of internal turmoil and low morale surface at {ticker}",
        "Activist investor targets {ticker}, demanding board changes",
    ]

    neutral_templates = [
        # Market & Stock Activity
        "{ticker} stock trades sideways on average volume",
        "Market awaits {ticker}'s upcoming earnings announcement",
        "Options activity increases for {ticker} ahead of {event}",
        "General market trends influence {ticker}'s price movement today",
        "{ticker} maintains position within the {index_name} index",
        "Analysts maintain 'Hold' rating on {ticker}",
        "Trading volume for {ticker} remains within historical norms",
        "Sector rotation impacts {ticker} stock performance",
        "{ticker} price consolidates after recent volatility",
        "Arbitrage opportunities noted in {ticker} derivatives",

        # Company Operations & Events
        "{ticker} to present at the upcoming {conference_name} conference",
        "Annual shareholder meeting scheduled for {ticker} next month",
        "{ticker} releases routine software patch for {product_name}",
        # "{ticker} confirms {executive_name} participation in industry panel",
        "Routine infrastructure maintenance announced by {ticker}",
        "{ticker} publishes white paper on {research_topic}",
        "Quarterly index rebalancing includes {ticker}",
        "{ticker} updates terms of service for {platform_name}",
        "{ticker} completes scheduled server upgrades",
        "Compliance report filed by {ticker} with the SEC",

        # General Business & Strategy
        "{ticker} continues R&D investment in {area}",
        "Speculation continues regarding {ticker}'s potential M&A targets",
        "Industry report highlights {ticker}'s position in the {market_segment} landscape",
        "{ticker} renews long-term supply agreement with {supplier_name}",
        "Changes to {ticker}'s board committee assignments announced",
        "{ticker} adjusts marketing spend for the upcoming quarter",
        "Discussions ongoing regarding {ticker}'s potential expansion into {new_area}",
        "Seasonal trends expected to influence {ticker}'s next quarter",
        "Currency exchange rates provide minor headwind/tailwind for {ticker}",
        "{ticker} workforce size remains stable",
        "Internal review of {business_process} underway at {ticker}",
        "Minor adjustments made to {ticker}'s pricing strategy",
        "{ticker} participates in joint industry research project",
        "Market commentary notes {ticker}'s stable dividend payout ratio",
        "{ticker}'s employee training programs updated",
    ]

    # --- Placeholder Values (Simple examples) ---
    placeholders = {
        "percent": [str(random.randint(5, 25))],
        "product_type": ["AI", "cloud", "mobile", "wearable", "EV", "gaming", "software"],
        "product_name": ["Platform X", "Device Z", "Service Pro", "ConnectSuite", "Quantum Chip"],
        "service_name": ["Cloud+", "StreamNow", "SecurePay", "AdPlatform"],
        "product_or_service": ["latest phone", "cloud platform", "AI assistant", "streaming service", "VR headset"],
        "area": ["quantum computing", "AI ethics", "metaverse development", "edge computing", "biotech AI"],
        "specific_achievement": ["energy efficiency", "data processing speed", "user accessibility"],
        "technology_field": ["holographic display", "neural interface", "fusion power", "graphene synthesis"],
        "platform_name": ["OS 15", "CloudSphere", "ConnectVerse", "Insight Engine"],
        "key_segment": ["enterprise software", "smartphone market", "cloud infrastructure", "digital advertising"],
        "region": ["Asia-Pacific", "European Union", "North America", "Latin America"],
        "acquired_company": ["Innovate Inc.", "DataCorp", "Synergy Systems"],
        "partner_company": ["Global Solutions Ltd.", "NextGen Tech", "Alpha Industries"],
        "investment_bank": ["Goldman Stanley", "Morgan Chase", "BoA Lynch"],
        "technology_area": ["facial recognition", "user data tracking", "AI decision-making"],
        "product_component": ["battery unit", "display panel", "processor chip", "charging port"],
        "competitor": ["TechGiant Co.", "Innovate Solutions", "Digital Dynamics"],
        "issue": ["privacy violations", "monopolistic practices", "product defects", "environmental damage"],
        "exec_name": ["J. Smith", "A. Lee", "M. Chen", "R. Garcia"],
        "event": ["earnings release", "product launch", "Fed meeting"],
        "index_name": ["S&P 500", "Nasdaq 100", "Dow Jones"],
        "conference_name": ["Global Tech Summit", "Innovate Now", "Future Forward Expo"],
        "research_topic": ["AI efficiency", "blockchain scalability", "quantum encryption"],
        "market_segment": ["cloud computing", "social media", "semiconductors", "e-commerce"],
        "supplier_name": ["ChipWorks", "Global Components", "Precision Parts"],
        "new_area": ["fintech services", "healthcare tech", "autonomous logistics"],
        "business_process": ["customer onboarding", "supply chain logistics", "talent acquisition"],
    }

    # --- Generate Headlines for Each Ticker ---
    headlines_by_ticker = {}
    tickers_to_generate = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA']

    # Ensure the requested ticker is included if not in the main list
    if ticker not in tickers_to_generate:
         tickers_to_generate.append(ticker)

    target_per_category = 20 # Aim for roughly 20 of each (pos, neg, neu) -> 60 total

    for t in tickers_to_generate:
        ticker_headlines = []
        # Add Positive
        for _ in range(target_per_category):
            template = random.choice(positive_templates)
            # Basic placeholder filling
            filled_template = template.format(
                ticker=t,
                **{k: random.choice(v) for k, v in placeholders.items()}
            )
            ticker_headlines.append(filled_template)

        # Add Negative
        for _ in range(target_per_category):
            template = random.choice(negative_templates)
            filled_template = template.format(
                ticker=t,
                **{k: random.choice(v) for k, v in placeholders.items()}
            )
            ticker_headlines.append(filled_template)

        # Add Neutral
        for _ in range(target_per_category):
            template = random.choice(neutral_templates)
            filled_template = template.format(
                ticker=t,
                **{k: random.choice(v) for k, v in placeholders.items()}
            )
            ticker_headlines.append(filled_template)

        # Add some specific flavor (examples) - Can be expanded significantly
        if t == "TSLA":
            ticker_headlines.extend([
                "Tesla lowers Model 3 prices in China amid competition",
                "Elon Musk tweets cryptic message about Tesla's future",
                "Tesla Full Self-Driving beta update receives mixed reviews",
                "Cybertruck production timeline remains uncertain",
                "Tesla hits milestone of 5 million vehicles produced",
            ])
        elif t == "AAPL":
             ticker_headlines.extend([
                "Speculation mounts about Apple's AR/VR headset launch date",
                "Apple emphasizes privacy features in new iOS update",
                "iPhone 16 design rumors surface online",
                "Apple expands its services bundle offering",
                "Right-to-repair legislation could impact Apple's service revenue",
             ])
        elif t == "NVDA":
             ticker_headlines.extend([
                 "Nvidia faces potential export restrictions on advanced AI chips",
                 "Demand for Nvidia GPUs remains strong in gaming and data centers",
                 "Nvidia collaborates with researchers on new AI models",
                 "Competitors challenge Nvidia's dominance in the AI hardware market",
                 "Nvidia's stock valuation comes under scrutiny",
             ])
        # Add similar specific lines for MSFT, GOOGL, AMZN, META...

        # Shuffle and store
        random.shuffle(ticker_headlines)
        headlines_by_ticker[t] = ticker_headlines

    # --- Return Result ---
    # Fallback for unknown tickers
    default_headlines = [f"{ticker} stock sees increased trading volume today."] * 5 + \
                        [f"Analysts issue mixed ratings for {ticker}."] * 5 + \
                        [f"Market awaits news from {ticker}."] * 5

    # Get headlines for the requested ticker, use default if not found
    selected_headlines = headlines_by_ticker.get(ticker, default_headlines)

    # Return the requested number of headlines
    return selected_headlines[:count]


# Example usage
if __name__ == "__main__":
    try:
        train_texts, test_texts, train_labels, test_labels = load_financial_phrasebank()
        print(f"Loaded {len(train_texts)} training samples and {len(test_texts)} test samples.")
    except Exception as e:
        print(f"Error: {str(e)}")
