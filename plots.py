def plot_bar(title: str, mapping: dict[str, float], xlabel: str, ylabel: str):
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        print('[UPOZORENJE] matplotlib nije instaliran:', e)
        return
    if not mapping:
        print('Nema podataka za grafikon.')
        return
    keys = list(mapping.keys())
    values = list(mapping.values())
    plt.figure()
    plt.bar(keys, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
